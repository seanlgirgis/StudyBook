import { writeFileSync } from "node:fs";
import OpenAI from "openai";

const client = new OpenAI(); // uses OPENAI_API_KEY from env

const res = await client.chat.completions.create({
  model: "gpt-4o-mini-audio-preview",
  modalities: ["text", "audio"],
  audio: { voice: "alloy", format: "wav" },
  messages: [{ role: "user", content: "Say: Hello from StudyBook audio test." }]
});

writeFileSync("hello.wav", Buffer.from(res.choices[0].message.audio.data, "base64"));
console.log("Saved hello.wav");
