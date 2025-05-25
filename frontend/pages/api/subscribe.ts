// legacy – kept blank because we insert directly from client
export default function handler(req, res) {
  res.status(404).json({error: 'Use Supabase insert'});
}
