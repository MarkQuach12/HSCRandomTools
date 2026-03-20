const { createClient } = require("@supabase/supabase-js");

async function ping() {
  const supabase = createClient(
    process.env.SUPABASE_URL,
    process.env.SUPABASE_KEY
  );

  const { data, error } = await supabase
    .from("Band 6 Data")
    .select("id")
    .limit(1);

  if (error) throw error;

  console.log("Ping successful:", JSON.stringify(data));
}

ping().catch((err) => {
  console.error("Error pinging Supabase:", err.message);
  process.exit(1);
});
