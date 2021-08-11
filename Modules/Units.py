SHIP_INFO = {
    # 함급으로 거꾸로 정렬
    "Scout": {
        "Firepower": 0,
        "DefensePoint": 3,
        "Cost": {
            "Iron": 4,
            "Oil": 1
        }  
    },
    "Frigate": {
        "Firepower": 1,
        "DefensePoint": 10,
        "Cost": {
            "Iron": 15,
            "Oil": 5
        }
    },
    "Destroyer": {
        "Firepower": 5,
        "DefensePoint": 30,
        "Cost": {
            "Iron": 60,
            "Oil": 20
        }
    },
    "Cruiser": {
        "Firepower": 25,
        "DefensePoint": 90,
        "Cost": {
            "Iron": 240,
            "Exot": 5
        }
    },
    "Battleship": {
        "Firepower": 125,
        "DefensePoint": 270,
        "Cost": {
            "Iron": 960,
            "Exot": 20
        }
    },
    "Carrier": {
        "Firepower": 600,
        "DefensePoint": 1100,
        "Cost": {
            "Iron": 3840,
            "Exot": 80
        }
    }
}

# 정찰함 4 iron  1 oil  3 hp 0 att
# 호위함  15 iron  5 oil  10 hp 1 att
# 구축함  60 iron  20 oil  30 hp  5 att
# 순양함  240 iron  5 exot  90 hp  25 att
# 전함    960 iron  20 exot  270 hp  125 att
# 우주모함 3840 iron  80 exot  1100 hp 600 att