
-- Supabase table for subscribers
create table if not exists public.subscribers (
  id uuid primary key default uuid_generate_v4(),
  email text not null unique,
  tickers text[] default '{}',
  kite_token text,
  created_at timestamptz default now()
);

-- Allow anon insert via Supabase public key
alter table public.subscribers enable row level security;
create policy "public insert" on public.subscribers
  for insert with check (true);
