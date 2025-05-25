
import { useState } from 'react';
import { createClient } from '@supabase/supabase-js';

const supabase = createClient(process.env.NEXT_PUBLIC_SUPABASE_URL!,
                              process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!);

export default function Home() {
  const [email, setEmail] = useState('');
  const [tickers, setTickers] = useState('');
  async function handle() {
    const { error } = await supabase
      .from('subscribers')
      .insert({ email, tickers: tickers.split(/[,\s]+/) });
    if (error) alert(error.message); else alert('Subscribed!');
  }
  return (
    <main className="p-10 max-w-xl mx-auto space-y-4">
      <h1 className="text-2xl font-bold">Indian Stocks Daily</h1>
      <input className="border p-2 w-full" placeholder="you@email.com"
             value={email} onChange={e=>setEmail(e.target.value)} />
      <input className="border p-2 w-full" placeholder="RELIANCE, INFY, TCS"
             value={tickers} onChange={e=>setTickers(e.target.value)} />
      <button className="bg-indigo-600 text-white px-4 py-2 rounded"
              onClick={handle}>Subscribe</button>
    </main>
  );
}
