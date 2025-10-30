#utf-8
"""SOC room logic: scan `auth.log`, aggregate failures by /24, extract top IP."""
from escaperoom.rooms.base import Room

class SOCRoom(Room):
    """SOC room."""
    
    def __init__(self):
        super().__init__(name="SOC room")

    def inspect(self, filepath, game_state):
        """Inspect the room's item and return output lines."""
        failwins = {}  # Our dictionary of failed attempts, it will have a sub dict for counts
        malformed_skipped = []  # our list of malformed lines that we've skipped
        log_entry_count = 0

        with open(filepath, "r") as f:
            # this r flag is very handy as it allows us to itterate across the lines in a for loop!
            for line in f:
                log_entry_count += 1

                retroencabulator = line.split()  # Take each line and push it to the variable retroencabulator

                try:  # I had to put this in a try block because sometimes the split would fail, if there wasn't a from in the line!
                    from_pos = retroencabulator.index("from")
                    ip = retroencabulator[from_pos + 1]
                except (ValueError, IndexError):
                    malformed_skipped.append(line.strip())
                    continue

                # Ip
                octs = ip.split(".")

                if len(octs) != 4 or not all(o.isdigit() and 0 <= int(o) <= 255 for o in octs):
                    malformed_skipped.append(line.strip())  # pop it into our list
                    continue

                if "Failed password" not in line:
                    continue
                else:

                    ip = retroencabulator[retroencabulator.index("from") + 1]
                    subnet = ".".join(ip.split(".")[:3]) + ".0/24"

                    if subnet not in failwins:
                        failwins[subnet] = {"counts": {}, "total": 0,
                                            "sample": line.strip()}  # counts is a dictionary within our failwins, allowing us to keep track of the number of failed attempts per IP

                    bucket = failwins[subnet]
                    bucket["counts"][ip] = bucket["counts"].get(ip, 0) + 1
                    bucket["total"] += 1

            top_subnet = None
            top_total = 0

            for subnet in failwins:
                total = failwins[subnet]["total"]
                if total > top_total:
                    top_total = total
                    top_subnet = subnet

            top_ip = None
            top_ip_count = 0
            # Get the counts, get the top IP
            for ip in failwins[top_subnet]["counts"]:
                count = failwins[top_subnet]["counts"][ip]
                if count > top_ip_count:
                    top_ip_count = count
                    top_ip = ip

            # The contract specifies "original log line", not just any example, so we need to ammend the sample using the top IP.
            try:
                with open("../../msc-group-03/auth.log", "r") as fh:
                    for ln in fh:
                        if "Failed password" in ln and f"from {top_ip} " in ln:
                            failwins[top_subnet]["sample"] = ln.strip()
                            break
            except FileNotFoundError:
                pass

            token = f"{top_ip.split('.')[-1].strip()}{top_total}"

            print("[Room SOC] Parsing logs...")
            print(top_total, "failed attempts found in", top_subnet)
            print("Top IP is", top_ip, "(last octet=", top_ip.split(".")[-1].strip(), ")")
            print(f"Token formed:", token)
            print()
            print(f"TOKEN[KEYPAD]={token}")
            print(f"EVIDENCE[KEYPAD].TOP24={top_subnet}")
            print(f"EVIDENCE[KEYPAD].COUNT={top_total}")
            print(f"EVIDENCE[KEYPAD].SAMPLE={failwins[top_subnet]['sample']}")
            print(f"EVIDENCE[KEYPAD].MALFORMED_SKIPPED={len(malformed_skipped)}")

        for _ in range(3):
            print("\a", end="", flush=True)  # EASTER EGG!
        return token





    # 1 Open auth.og

    # create datastrucures for failed attemps, malformed lines, and as a bonus for our metrics a long entry count

    # 2 for each line:
    # try to parse it
    # if it looks like a "failed password" line:
    # extract IPs
    # Identify the /24s with the most failures (attacking subnet)
    # From within that group find the most attacking IP

#
# Transcript contract (required lines):
# TOKEN[KEYPAD]=<code>
# EVIDENCE[KEYPAD].TOP24=<cidr>/24
# EVIDENCE[KEYPAD].COUNT=<int>
# EVIDENCE[KEYPAD].SAMPLE=<full original log line>
# EVIDENCE[KEYPAD].MALFORMED_SKIPPED=<int>
# Skills practiced: file I/O, dictionaries, string splitting, exception handling