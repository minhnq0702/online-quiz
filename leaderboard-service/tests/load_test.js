import { check, sleep } from "k6";
import http from "k6/http";

export const options = {
  // vus: 50,
  // duration: "10s",

  stages: [
    { duration: "10s", target: 200 },
    { duration: "30s", target: 500 },
    { duration: "60s", target: 0 },
  ],
};

const payload = JSON.stringify({
  quiz_id: 0,
  username: "string",
  score: 0,
});

export default async function () {
  const USER_ID = 2;

  const url = `http://localhost:8000/leaderboard/1?limit=20&user_id=${USER_ID}`;
  const read = http.get(url);
  // console.log("The user current rank is", read.body["user_rank"]["rank"]);
  const rank = read.json()["user_rank"];
  console.log(
    `The current RANK of USER ${USER_ID} is ${rank["rank"]} with score ${rank["score"]}`
  );

  check(read, {
    "status is 200": (r) => r.status === 200 || r.status === 201,
    "response time is < 200ms": (r) => r.timings.duration <= 200,
    "response time is < 500ms": (r) => 200 < r.timings.duration < 500,
    "response time is < 1000ms": (r) => 500 <= r.timings.duration < 1000,
    "response time too slow": (r) => 1000 <= r.timings.duration,
  });

  sleep(0.2);
}
