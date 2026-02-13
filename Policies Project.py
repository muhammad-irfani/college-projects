import csv

def load_policies(file_path):
    """
    Load policies from a CSV file.
    """
    with open(file_path, newline='', encoding='utf-8') as csvfile:
       
        raw_content = csvfile.read()
        print(f"[DEBUG] Raw CSV content:\n{raw_content}")  # Debugging: Print raw CSV content
        
       
        csvfile.seek(0)
        
        reader = csv.DictReader(csvfile)
        
        # Debugging: Checking headers
        headers = reader.fieldnames
        print(f"[DEBUG] CSV Headers: {headers}")  # Printing headers for debugging
        
        policies = list(reader)
        
        
        for policy in policies:
            policy = {key.strip(): value.strip() for key, value in policy.items()}
        
        # Debugging: Printing the loaded policies
        print("[DEBUG] Loaded policies:")
        for policy in policies:
            print(policy)

    return policies


def check_access(role, permission, obj, policies):
    """
    Check if the requested access matches a policy in the list.
    """
    print(f"[DEBUG] Checking access for: Role={role}, Permission={permission}, Object={obj}")
    
    for entry in policies:
        print(f"[DEBUG] Checking policy: {entry}")  # Debugging: Printing each policy being checked
        if (entry['role'].lower() == role.lower() and 
            (entry['permission'].lower() == permission.lower() or entry['permission'].lower() == 'all') and 
            (entry['object'].lower() == obj.lower() or entry['object'].lower() == 'all')):
            return True, entry
    
    return False, None


def main():
    """
    Main function to load policies and check user access.
    """
    policies = load_policies('data_policies.csv')

    role = input("Enter your role: ")
    permission = input("Enter requested permission (view/edit): ")
    obj = input("Enter target object: ")

    # Debugging: Printing user inputs
    print(f"[DEBUG] User input - Role: {role}, Permission: {permission}, Object: {obj}")

    allowed, rule = check_access(role, permission, obj, policies)

    if allowed:
        print(f"ACCESS GRANTED: Rule matched - ({rule['role']}, {rule['permission']}, {rule['object']})")
    else:
        print("ACCESS DENIED: No matching rule found.")


if __name__ == "__main__":
    main()
