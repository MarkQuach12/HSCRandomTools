const { createClient } = require("@supabase/supabase-js");

async function ping() {
  const url = process.env.SUPABASE_URL;
  const key = process.env.SUPABASE_KEY;

  console.log("SUPABASE_URL defined:", !!url);
  console.log("SUPABASE_KEY defined:", !!key);

  if (!url || !key) {
    throw new Error("Missing SUPABASE_URL or SUPABASE_KEY environment variables");
  }

  const supabase = createClient(url, key);

  const { data, error } = await supabase
    .from("Band 6 Data")
    .select("id")
    .limit(1);

  if (error) throw error;

  console.log("Ping successful:", JSON.stringify(data));
}

ping().catch((err) => {
  console.error("Error pinging Supabase:", err);
  if (err.cause) {
    console.error("Cause:", err.cause);
  }
  process.exit(1);
});
