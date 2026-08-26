-- DM automatica — schema completo. Rodar no SQL Editor do Supabase (uma vez).
-- Todas as tabelas ficam com RLS ligado e SEM políticas: acesso só pelo servidor,
-- usando a service_role key (que ignora RLS). O navegador nunca toca no banco.

create extension if not exists pgcrypto;

-- ---------------------------------------------------------------- config
-- Linha única (id sempre 1) com o token e a identidade da conta conectada.
create table if not exists config (
  id                  smallint primary key default 1 check (id = 1),
  ig_user_id          text,
  ig_username         text,
  ig_name             text,
  profile_picture_url text,
  access_token        text,
  token_expires_at    timestamptz,
  updated_at          timestamptz not null default now()
);

-- ----------------------------------------------------------- automations
create table if not exists automations (
  id                     uuid primary key default gen_random_uuid(),
  nome                   text        not null,
  ativo                  boolean     not null default true,

  -- gatilhos
  trigger_comment        boolean     not null default true,
  trigger_story          boolean     not null default false,
  trigger_dm             boolean     not null default false,

  -- casamento de palavra-chave
  keywords               text[]      not null default '{}',
  match_type             text        not null default 'contains'
                                     check (match_type in ('contains','exact','any')),
  media_id               text,       -- post/reels específico. null = qualquer post

  -- resposta pública no comentário (sorteia entre as variações)
  public_replies         text[]      not null default '{}',

  -- primeira DM (resposta privada — fura a janela de 24h)
  welcome_text           text        not null,
  quick_reply_label      text,       -- botão que a pessoa toca pra abrir a janela

  -- entrega do lead magnet
  link_text              text,
  link_button_label      text,
  link_url               text,

  -- lembrete
  reminder_text          text,
  reminder_delay_minutes integer     not null default 60,

  created_at             timestamptz not null default now(),
  updated_at             timestamptz not null default now()
);

-- ------------------------------------------------------------- followups
-- A sequência de envio derivada da automação. Regerada a cada save.
create table if not exists followups (
  id            uuid primary key default gen_random_uuid(),
  automation_id uuid not null references automations(id) on delete cascade,
  step          integer not null,
  kind          text    not null check (kind in ('link','reminder')),
  delay_minutes integer not null default 0,
  payload       jsonb   not null,
  unique (automation_id, step)
);

-- -------------------------------------------------------------- contacts
create table if not exists contacts (
  ig_id              text primary key,
  username           text,
  first_seen_at      timestamptz not null default now(),
  last_reply_at      timestamptz,          -- toque da pessoa: abre a janela de 24h
  last_automation_id uuid references automations(id) on delete set null,
  updated_at         timestamptz not null default now()
);

-- ----------------------------------------------------------------- queue
create table if not exists queue (
  id                   uuid primary key default gen_random_uuid(),

  -- pra quem: comment_id (resposta privada) ou id (DM normal)
  recipient_kind       text not null check (recipient_kind in ('comment_id','id')),
  recipient_value      text not null,

  contact_ig_id        text,
  automation_id        uuid references automations(id) on delete set null,
  kind                 text not null check (kind in ('welcome','link','reminder','public_reply')),

  payload              jsonb not null,      -- corpo já montado pro endpoint
  requires_open_window boolean not null default true,

  run_after            timestamptz not null default now(),
  status               text not null default 'pending'
                       check (status in ('pending','sending','sent','failed','skipped')),
  attempts             integer not null default 0,
  claimed_at           timestamptz,
  error                text,

  -- impede envio duplicado do mesmo passo pro mesmo evento
  dedupe_key           text unique,

  created_at           timestamptz not null default now(),
  sent_at              timestamptz
);

create index if not exists queue_ready_idx on queue (status, run_after);

-- ---------------------------------------------------------------- events
create table if not exists events (
  id          bigserial primary key,
  kind        text,
  payload     jsonb,
  received_at timestamptz not null default now()
);

create index if not exists events_received_idx on events (received_at desc);

-- ------------------------------------------------- trava atômica da fila
-- Marca até `batch` itens como 'sending' e devolve. SKIP LOCKED garante que
-- duas execuções simultâneas (webhook + cron) nunca peguem o mesmo item.
create or replace function claim_queue(batch integer default 10)
returns setof queue
language sql
as $$
  update queue q
     set status     = 'sending',
         claimed_at = now(),
         attempts   = q.attempts + 1
   where q.id in (
     select id from queue
      where status = 'pending'
        and run_after <= now()
      order by run_after
      limit batch
      for update skip locked
   )
  returning q.*;
$$;

-- Item que ficou preso em 'sending' (deploy caiu no meio) volta pra fila.
create or replace function requeue_stuck(minutes integer default 5)
returns integer
language sql
as $$
  with volta as (
    update queue
       set status = 'pending', claimed_at = null
     where status = 'sending'
       and claimed_at < now() - make_interval(mins => minutes)
       and attempts < 3
    returning 1
  )
  select count(*)::int from volta;
$$;

-- -------------------------------------------------------------------- RLS
alter table config      enable row level security;
alter table automations enable row level security;
alter table followups   enable row level security;
alter table contacts    enable row level security;
alter table queue       enable row level security;
alter table events      enable row level security;
