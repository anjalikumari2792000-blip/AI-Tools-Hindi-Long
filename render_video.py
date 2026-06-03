# --- N8N RESUME LOGIC WITH ROBUST RETRY (NO THIRD-PARTY RELAY) ---
if resume_url:
    print(f"Resuming n8n workflow at: {resume_url}")
    
    # Session aur Retry logic set up karna
    # total=5: 5 baar try karega connection fail hone par
    # backoff_factor=2: har fail ke baad wait time badhega (2s, 4s, 8s, 16s...) taaki server temporary block hatane ka time de
    session = requests.Session()
    retry_strategy = Retry(
        total=5,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["POST"],
        backoff_factor=2
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount('https://', adapter)
    session.mount('http://', adapter)

    try:
        # verify=False add kiya gaya hai SSL errors ignore karne ke liye, timeout 60 seconds hai
        response = session.post(resume_url, json={"body": payload}, headers=safe_headers, timeout=60, verify=False)
        print(f"n8n Resume Response: {response.status_code} - {response.text}")
    except requests.exceptions.RetryError as e:
        print(f"CRITICAL ERROR: 5 retries ke baad bhi Hostinger VPS ne connection accept nahi kiya. Firewall IP block kar raha hai. Error: {e}")
    except Exception as e:
        print(f"Warning: Failed to resume n8n. Error: {e}")
else:
    print("No RESUME_URL provided by n8n.")
