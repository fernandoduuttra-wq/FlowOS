-- DM automatica — o motor sem custo.
--
-- A Vercel no plano grátis (Hobby) não roda cron de minuto. Então quem bate o
-- ponto é o Postgres do Supabase: pg_cron agenda, pg_net faz o HTTP.
--
-- RODAR DEPOIS DO DEPLOY, trocando os dois placeholders abaixo:
--   {APP_URL}      -> https://seu-app.vercel.app  (sem barra no fim)
--   {CRON_SECRET}  -> o mesmo valor da env CRON_SECRET na Vercel

create extension if not exists pg_cron;
create extension if not exists pg_net;

-- Drena a fila a cada minuto (rede de segurança; o envio rápido vem do webhook).
select cron.schedule(
  'dmauto-drain',
  '* * * * *',
  $$
  select net.http_post(
    url     := '{APP_URL}/api/drain',
    headers := '{"Content-Type":"application/json","x-cron-secret":"{CRON_SECRET}"}'::jsonb,
    body    := '{}'::jsonb
  );
  $$
);

-- Renova o token de 60 dias toda segunda às 03:00 UTC (00:00 em São Paulo).
select cron.schedule(
  'dmauto-refresh-token',
  '0 3 * * 1',
  $$
  select net.http_post(
    url     := '{APP_URL}/api/cron/refresh-token',
    headers := '{"Content-Type":"application/json","x-cron-secret":"{CRON_SECRET}"}'::jsonb,
    body    := '{}'::jsonb
  );
  $$
);

-- Conferir:            select * from cron.job;
-- Ver as execuções:    select * from cron.job_run_details order by start_time desc limit 20;
-- Desagendar:          select cron.unschedule('dmauto-drain');
