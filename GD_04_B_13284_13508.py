import matplotlib.pyplot as plt

peta_1 = [
    ["S", " ", " ", " ", "G"],
    ["#", "#", "#", "#", " "],
    [" ", " ", " ", " ", " "],
    [" ", " ", " ", " ", " "],
    [" ", " ", " ", " ", " "]
]

peta_2 = [
    ["S", " ", " ", "#", "G"],
    ["#", "#", " ", "#", " "],
    [" ", " ", " ", " ", " "],
    [" ", "#", "#", "#", " "],
    [" ", " ", " ", " ", " "]
]

peta_3 = [
    ["S", " ", " ", " ", " ", "#", "G"],
    [" ", " ", "#", "#", " ", "#", " "],
    [" ", " ", "#", "#", " ", "#", " "],
    ["#", " ", " ", "#", "#", "#", " "],
    [" ", " ", " ", " ", " ", " ", " "]
]

peta_4 = [
    ["S", " ", "#", " ", " ", " ", "#", " ", " ", " "],
    ["#", " ", "#", " ", "#", " ", "#", " ", "#", " "],
    [" ", " ", " ", " ", "#", " ", " ", " ", "#", " "],
    [" ", "#", "#", " ", "#", "#", " ", "#", "#", " "],
    [" ", " ", " ", " ", " ", " ", " ", "#", " ", " "],
    ["#", "#", "#", "#", "#", " ", " ", "#", " ", "#"],
    [" ", " ", " ", " ", "#", " ", "#", "#", " ", " "],
    [" ", "#", "#", " ", "#", " ", " ", " ", " ", "#"],
    [" ", " ", " ", " ", " ", "#", "#", "#", " ", " "],
    ["#", "#", "#", "#", " ", " ", " ", " ", " ", "G"]
]

environment_map = peta_4

class BaseAgent:

    def __init__(self, env):

        self.env = [row[:] for row in env]
        self.x, self.y = self.find_symbol("S")
        self.goal_x, self.goal_y = self.find_symbol("G")
        self.path = [(self.x, self.y)]
        self.steps = 0

    def find_symbol(self, symbol):

        for i, row in enumerate(self.env):
            for j, cell in enumerate(row):
                if cell == symbol:
                    return i, j
        return -1, -1

    def display(self):

        for i in range(len(self.env)):

            row = ""

            for j in range(len(self.env[0])):
                if i == self.x and j == self.y:
                    row += " A "
                else:
                    row += f" {self.env[i][j]} "

            print(row)

        print("-" * 25)

    def choose_action(self):
        return 0, 0

    def run(self, max_steps=100):
        print("=" * 50)
        print(
            f"=== {self.__class__.__name__.replace('Agent', ' Agent').upper()} ==="
        )

        print("=" * 50)

        print("Posisi awal:")
        self.display()

        while (
            self.env[self.x][self.y] != "G"
            and self.steps < max_steps
        ):

            dx , dy = self.choose_action()

            self.x += dx
            self.y += dy

            self.path.append((self.x, self.y))
            self.steps += 1

            print(f"Langkah ke-{self.steps}:")

            self.display()

        return self.steps

class SimpleReflexAgent(BaseAgent):

    def choose_action(self):

        possible_moves = [
            (1, 0),
            (0, 1),
            (-1, 0),
            (0, -1)
        ]

        for dx, dy in possible_moves:

            nx = self.x + dx
            ny = self.y + dy

            if (
                0 <= nx < len(self.env)
                and 0 <= ny < len(self.env[0])
                and self.env[nx][ny] != "#"
            ):
                return dx, dy

        return 0, 0
    

class ModelBasedReflexAgent(BaseAgent):

    def __init__(self, env):

        super().__init__(env)
        self.visited = set()

    def choose_action(self):

        self.visited.add((self.x, self.y))

        possible_moves = [
            (1, 0),
            (0, 1),
            (-1, 0),
            (0, -1)
        ]

        for dx, dy in possible_moves:

            nx = self.x + dx
            ny = self.y + dy

            if (
                0 <= nx < len(self.env)
                and 0 <= ny < len(self.env[0])
                and self.env[nx][ny] != "#"
                and (nx, ny) not in self.visited
            ):
                return dx, dy
            
        for dx, dy in possible_moves:

            nx = self.x + dx
            ny = self.y + dy

            if (
                0 <= nx < len(self.env)
                and 0 <= ny < len(self.env[0])
                and self.env[nx][ny] != "#"
            ):
                return dx, dy

        return 0, 0

class GoalBasedAgent(BaseAgent):

    def choose_action(self):

        diff_x = self.goal_x - self.x
        diff_y = self.goal_y - self.y

        if abs(diff_x) > abs(diff_y):

            move_x = 1 if diff_x > 0 else -1
            move_y = 0

        else:

            move_x = 0
            move_y = 1 if diff_y > 0 else -1

        nx = self.x + move_x
        ny = self.y + move_y

        if (
            0 <= nx < len(self.env)
            and 0 <= ny < len(self.env[0])
            and self.env[nx][ny] != "#"
        ):
            return move_x, move_y
        
        possible_moves = [
            (1, 0),
            (0, 1),
            (-1, 0),
            (0, -1)
        ]

        for dx, dy in possible_moves:

            nx = self.x + dx
            ny = self.y + dy

            if (
                0 <= nx < len(self.env)
                and 0 <= ny < len(self.env[0])
                and self.env[nx][ny] != "#"
            ):
                return dx, dy

        return 0, 0

class UtilityBasedAgent(BaseAgent):

    def calculate_utility(self, x, y):

        distance = (
            abs(self.goal_x - x)
            + abs(self.goal_y - y)
        )

        return -distance

    def choose_action(self):

        possible_moves = [
            (1, 0),
            (0, 1),
            (-1, 0),
            (0, -1)
        ]

        best_utility = float("-inf")

        best_move = (0, 0)

        for dx, dy in possible_moves:

            nx = self.x + dx
            ny = self.y + dy

            if (
                0 <= nx < len(self.env)
                and 0 <= ny < len(self.env[0])
                and self.env[nx][ny] != "#"
            ):

                utility = self.calculate_utility(nx, ny)

                if utility > best_utility:

                    best_utility = utility
                    best_move = (dx, dy)

        return best_move

def evaluate(agent_class, env_map, max_steps=100):

    agent = agent_class(env_map)

    steps = agent.run(max_steps)

    success = agent.env[agent.x][agent.y] == "G"

    return {
        "name": agent_class.__name__,
        "steps": steps,
        "success": success,
        "position": (agent.x, agent.y),
        "path": agent.path
    }

agents = [
    SimpleReflexAgent,
    ModelBasedReflexAgent,
    GoalBasedAgent,
    UtilityBasedAgent
]

results = []

for agent in agents:

    result = evaluate(
        agent,
        environment_map
    )

    results.append(result)


print("=" * 65)
print("HASIL PERBANDINGAN PERFORMA AGEN")
print("=" * 65)

for result in results:

    print(f"\nNama Agen       : {result['name']}")
    print(f"Jumlah Langkah  : {result['steps']}")

    if result["success"]:
        print("Status          : Berhasil mencapai Goal")
    else:
        print("Status          : Gagal mencapai Goal")

    print(f"Posisi Akhir    : {result['position']}")
    print(f"Jalur           : {result['path']}")

    print("-" * 65)


nama_agen = [
    result["name"].replace("Agent", "")
    for result in results
]

jumlah_langkah = [
    result["steps"]
    for result in results
]

plt.figure(figsize=(10, 6))

bars = plt.bar(
    nama_agen,
    jumlah_langkah
)

for bar in bars:
    nilai = bar.get_height()

    plt.text(
        bar.get_x() + bar.get_width() / 2,
        nilai,
        str(int(nilai)),
        ha="center",
        va="bottom"
    )

plt.title("Perbandingan Performa Empat Jenis Agen")

plt.xlabel("Jenis Agen")
plt.ylabel("Jumlah Langkah")
plt.grid(axis="y", linestyle="--", alpha=0.7)
plt.show()


