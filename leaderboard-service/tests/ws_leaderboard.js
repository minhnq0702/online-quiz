import { check } from "k6";
import ws from "k6/ws";

export const options = {
  //   vus: 500,
  //   duration: "20s",
  stages: [
    { duration: "30s", target: 200 },
    { duration: "1m", target: 500 },
    { duration: "30s", target: 0 },
  ],
};

export default function () {
  const url =
    "ws://localhost:8000/leaderboard/ws/statistic/1?limit=20&user_id=2";
  //   const params = { tags: { my_tag: "hello" } };

  const res = ws.connect(url, {}, function (socket) {
    socket.on("open", () => console.log("connected"));
    socket.on("message", (data) => {
      const resp = JSON.parse(data);
      const leaderboard = resp["top_ranks"];
      const rank = resp["user_rank"];
      console.log(
        `Top 1: ${leaderboard[0].user_id} with score ${leaderboard[0].score}`
      );
      console.log(`Rank of USER_ID=2 is ${rank.rank} with score ${rank.score}`);
    });
    setTimeout(() => {
      socket.close();
    }, 8000);
    socket.on("close", () => console.log("disconnected"));
  });

  check(res, { "status is 101": (r) => r && r.status === 101 });
}
