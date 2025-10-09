
# 1 Lobby 
    Game engine, a state machine, take CLI commands to move through the room
    
    Read–Eval–Print Loop

    Running python escape.py --start intro --transcript run.txt starts
    an interactive REPL (Read–Eval–Print Loop)
    Commands supported: look , move <room> , inspect <item> , use
    <item> , inventory , hint , save , load , quit .

# 2 SOC Triage
    
    Auth.log

    The SSH logs show repeated authentication failures. Our task is to identify the most
    likely attacking subnet.

    1. Parse auth.log line-by-line.
    2. Tolerate malformed lines, skip them but count how many were skipped.
    3. For each Failed password line, extract the source IP and group by /24 (first
    three octets).
    4. Identify the /24 with the largest number of failures.
    5. Within that /24 , choose the IP that occurred most frequently, take its last octet
    L .
    6. Form the keypad code token: "{L}{COUNT}" where COUNT is the failure count in
    that /24 .

    Transcript contract (required lines):
    TOKEN[KEYPAD]=<code>
    EVIDENCE[KEYPAD].TOP24=<cidr>/24
    EVIDENCE[KEYPAD].COUNT=<int>
    EVIDENCE[KEYPAD].SAMPLE=<full original log lin




# 3 DNS Closet Config 
    
    Data: dns.cfg

    1. Parse a key=value file robustly (allow extra spaces and # comments)
    2. For keys hint1..hintN , attempt to decode values as base64 (catch exceptions
    where decoding fails)
    3. token_tag=X indicates the single hintX whose decoded last word is the token
    
    Transcript contract:
    TOKEN[DNS]=<word>
    EVIDENCE[DNS].KEY=hintX
    EVIDENCE[DNS].DECODED_LINE=<decoded sentenc
    Incident responders decode obfuscated
    hints in configs
    Vault Corridor Regex search & validation
    Forensics sift through dumps for valid
    artifacts
    Room Represents Real-world parallel
    Malware Lab Graph traversal Threat hunters trace malware process trees
    Final Gate Verification & reporting Teams must package findings into proof

# 4 Vault Corridor
   
    Data: vault_dump.txt 
    
    A noisy dump contains a safe code SAFE{a-b-c} , only one candidate satisfies the
    checksum a+b==c

    1. Precompile a regex that captures SAFE{a-b-c} tolerant to whitespace and
    newlines.
    2. Find candidates and validate a+b==c (integers)

    Transcript contract:
    TOKEN[SAFE]=a-b-c
    EVIDENCE[SAFE].MATCH="SAFE{a-b-c}"
    EVIDENCE[SAFE].CHECK=a+b=c

# 5 Malware Lab

    Data: proc_tree.jsonl

    A process tree contains a malicious chain ending with an exfil command ( curl or
    scp ).
    
    
    1. Read JSON-lines, build adjacency children map children[ppid] ->
    list[pid] .
    2. Implement DFS (recursive) and BFS (iterative) routines, use a visited set to
    avoid cycles
    3. Starting from a given PID (stated in the room text), find any path that ends in a cmd
    containing curl or scp .
    4. Token is the terminal PID of that path.

    Transcript contract:
    TOKEN[PID]=<pid>
    EVIDENCE[PID].PATH=[p0->p1->...->pid]
    EVIDENCE[PID].CMD="<matched command>"
    Skills practiced: graphs, recursion, complexity analysis, robust JSON parsing

#  6 Final Gate 
    
    Data: final_gate.txt

    The exit checks cryptographic integrity of tokens.
    Student task:
    Read final_gate.txt for the required token_order , group_id , and
    expected_hmac .
    Combine your tokens in the correct order to form the message:
    group_id|token1-token2-token3-token4
    Output the message and the expected HMAC from the file.
    Mark the gate as pending. The instructor will verify during the demo.

    Transcript contract:
    FINAL_GATE=PENDING
    MSG=<group_id|token1-token2-token3-token4>
    EXPECTED_HMAC=<hex from final_gate.txt> 

