# TEST CASES

## Functional Requirements

| Test Case ID | Description                           | Pre-conditions            | Steps                          | Expected Result                   |
|---------------|---------------------------------------|---------------------------|----------------------------------|------------------------------------|
| FR-1          | User can register                    | None                      | 1. Go to the registration page  
2. Fill in required details  
3. Submit the form | User is registered and logged in |
| FR-2          | User can log in                       | User must be registered   | 1. Go to the login page        
2. Enter credentials  
3. Click login | User is logged in successfully     |
| FR-3          | User can add a book                  | User must be logged in    | 1. Go to add book page         
2. Fill in book details  
3. Submit  | Book is added to the system       |

## Non-Functional Requirements

| Test Case ID | Description                           | Metrics                   | Expected Outcome                 |
|---------------|---------------------------------------|---------------------------|------------------------------------|
| NFR-1        | System response time                  | < 2 seconds               | System responds in less than 2 seconds |
| NFR-2        | System should handle 1000 concurrent users | Concurrent users        | System handles 1000 users without crashing |
| NFR-3        | System uptime                         | 99.9%                      | System is operational 99.9% of the time |