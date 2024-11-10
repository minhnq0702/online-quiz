import { check, sleep } from "k6";
import http from "k6/http";

export const options = {
  // vus: 50,
  // duration: "10s",
  stages: [
    { duration: "30s", target: 20 },
    { duration: "1m", target: 50 },
    { duration: "30s", target: 0 },
  ],
};

const payload = JSON.stringify({
  quiz_id: 0,
  username: "string",
  score: 0,
});

export default async function () {
  const url = "http://localhost:8000/leaderboard";
  // const create = http.post(url, payload, {
  //   headers: {
  //     "Content-Type": "application/json",
  //   },
  // });
  const read = http.get(url);
  // await Promise.all([create, read]);

  // check(create, {
  //   "status is 200": (r) => r.status === 200 || r.status === 201,
  //   "response time is < 500ms": (r) => r.timings.duration < 500,
  // });

  check(read, {
    "status is 200": (r) => r.status === 200 || r.status === 201,
    "response time is < 500ms": (r) => r.timings.duration < 500,
  });

  sleep(0.2);
}
