# Cyber Security Assignments

print("Cyber Security Assignments")
print("========================")

# 1. Encrypt the message "HELLO" using a Caesar cipher with a shift of 4. 
# Then, decrypt the ciphertext "Lipps" using the reverse shift.
print("1. Caesar Cipher Encryption/Decryption")

# Simple Caesar cipher function
def encrypt_caesar(text, shift):
    result = ""
    for char in text:
        if char.isalpha():
            # Handle uppercase letters
            if char.isupper():
                result += chr((ord(char) - ord('A') + shift) % 26 + ord('A'))
            # Handle lowercase letters
            else:
                result += chr((ord(char) - ord('a') + shift) % 26 + ord('a'))
        else:
            result += char
    return result

def decrypt_caesar(text, shift):
    # To decrypt, use negative shift
    return encrypt_caesar(text, -shift)

# Encrypt "HELLO" with shift of 4
original_text = "HELLO"
shift = 4
encrypted = encrypt_caesar(original_text, shift)
print(f"Original text: {original_text}")
print(f"Encrypted text: {encrypted}")

# Decrypt "Lipps" with reverse shift (shift of -4)
ciphertext = "Lipps"
decrypted = decrypt_caesar(ciphertext, shift)
print(f"Ciphertext: {ciphertext}")
print(f"Decrypted text: {decrypted}")

print()

# Note: For assignment 2 about OpenSSL, we'll provide the commands as they would be used in a real environment
print("2. OpenSSL RSA Key Generation (Commands to run in terminal):")
print("   openssl genrsa -out private_key.pem 2048")
print("   openssl rsa -in private_key.pem -pubout -out public_key.pem")
print("   cat private_key.pem  # To view private key")
print("   cat public_key.pem   # To view public key")
print()

print("Operating System Security:")
print("-" * 25)

print("1. Linux user account creation and file permissions (Commands to run in terminal):")
print("   # Create two users")
print("   sudo useradd user1")
print("   sudo useradd user2")
print("   sudo passwd user1  # Set password for user1")
print("   sudo passwd user2  # Set password for user2")
print()
print("   # Create a file and set permissions")
print("   touch secure_file.txt")
print("   sudo chown user1:user1 secure_file.txt")
print("   sudo chmod 600 secure_file.txt  # Only user1 can read and write")
print("   # user2 will have no access to the file")
print()

print("2. Disable SSH root login (Commands to run in terminal):")
print("   # Edit SSH configuration")
print("   sudo nano /etc/ssh/sshd_config")
print("   # Find and change: PermitRootLogin no")
print("   # Save and restart SSH service")
print("   sudo systemctl restart sshd")
print("   # Verify by trying to SSH as root from another machine")
print()

print("Network Security & VPNs:")
print("-" * 25)

print("1. OpenVPN setup commands (Commands to run in terminal):")
print("   # Install OpenVPN")
print("   sudo apt-get install openvpn")
print("   # Connect to VPN")
print("   sudo openvpn --config client.ovpn")
print("   # Check IP before and after connection")
print("   curl ifconfig.me")
print()

print("2. Nmap port scanning (Commands to run in terminal):")
print("   # Scan for open ports on target machine")
print("   nmap -sS -sV target_ip_address")
print("   # Identify services on open ports")
print("   nmap -sV -p port1,port2,port3 target_ip_address")
print()

print("Web Application Security:")
print("-" * 27)

print("1. SQL Injection example (Conceptual - to be used on vulnerable apps like DVWA):")
print("   # Example payload: ' OR '1'='1")
print("   # In login form, enter: admin'-- in username field")
print()

print("2. XSS Attack example (Conceptual - to be used on vulnerable apps):")
print("   # Inject: <script>alert('XSS')</script> in form fields")
print("   # For persistent XSS, this script would be stored in database")
print()

print("Ethical Hacking & Penetration Testing:")
print("-" * 40)

print("1. Whois and nslookup commands (Commands to run in terminal):")
print("   # Get domain information")
print("   whois example.com")
print("   # Get IP and DNS info")
print("   nslookup example.com")
print("   # Alternative")
print("   dig example.com")
print()

print("2. Metasploit Framework usage (Commands to run in terminal):")
print("   # Start Metasploit")
print("   msfconsole")
print("   # Search for MS08-067 vulnerability")
print("   search ms08_067")
print("   # Use exploit")
print("   use exploit/windows/smb/ms08_067_netapi")
print("   # Set target and payload")
print("   set RHOST target_ip")
print("   set payload windows/meterpreter/reverse_tcp")
print("   # Execute exploit")
print("   exploit")
print()

print("Malware Analysis & Reverse Engineering:")
print("-" * 42)

print("1. Strings command to extract text from malware (Commands to run in terminal):")
print("   # Extract readable strings from malware sample")
print("   strings malware_sample.exe")
print("   # Look for URLs, IP addresses, commands")
print("   strings malware_sample.exe | grep -E 'http|www|[0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}'")
print()

print("2. Sandbox environment setup (Conceptual):")
print("   # Use tools like:")
print("   # - VirtualBox/VMware for isolated environment")
print("   # - Process Monitor (ProcMon) for file/registry/network monitoring")
print("   # - Wireshark for network traffic analysis")
print("   # - Sandboxie for file system monitoring")
print()

print("Incident Response & Digital Forensics:")
print("-" * 40)

print("1. Simulate security breach and audit log (Commands to run in terminal):")
print("   # Create a malicious script")
print("   echo 'echo \"Security breach simulated\" > /tmp/breach_log.txt' > malicious_script.sh")
print("   # Make it executable")
print("   chmod +x malicious_script.sh")
print("   # Run the script")
print("   ./malicious_script.sh")
print("   # Check audit logs")
print("   sudo ausearch -m all -ts recent")
print()

print("2. Analyze system logs for suspicious activity (Commands to run in terminal):")
print("   # Check authentication logs")
print("   sudo cat /var/log/auth.log | grep -i 'failed\\|invalid\\|error'")
print("   # Check for suspicious login attempts")
print("   sudo grep -E 'Failed|Invalid' /var/log/auth.log")
print("   # Get IP addresses of failed attempts")
print("   sudo grep 'Failed password' /var/log/auth.log | awk '{print $11}' | sort | uniq -c")
print()

print("Cloud & IoT Security:")
print("-" * 22)

print("1. AWS/Google Cloud firewall configuration (Conceptual):")
print("   # In AWS Console:")
print("   # 1. Go to EC2 -> Security Groups")
print("   # 2. Create new security group")
print("   # 3. Add rules: Allow HTTP (port 80) and SSH (port 22)")
print("   # 4. Deny all other ports")
print("   # 5. Apply to your instance")
print()

print("2. IoT device traffic analysis (Conceptual):")
print("   # Connect IoT devices to network")
print("   # Start Wireshark capture")
print("   # Capture: sudo wireshark")
print("   # Filter for IoT device IPs")
print("   # Look for unencrypted traffic (HTTP instead of HTTPS)")
print("   # Check for default passwords and unsecured protocols")
print()

print()
print("Note: These are the basic approaches for each assignment.")
print("Always make sure you have permission before doing any security testing.")
print("Practice on your own systems or approved test environments only.")