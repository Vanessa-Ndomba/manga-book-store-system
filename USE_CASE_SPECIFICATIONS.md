# Use Case Specifications

## Use Case 1: User Registration
**Preconditions:** User is not registered.
**Postconditions:** User account is created.
**Basic Flow:** 1. User navigates to the registration page. 2. User fills out the registration form and submits. 3. System validates the input and creates a new user account.
**Alternative Flows:** 1. Invalid input is entered. (User is prompted to correct the input.)

## Use Case 2: User Login
**Preconditions:** User is registered.
**Postconditions:** User is authenticated and logged in.
**Basic Flow:** 1. User navigates to the login page. 2. User enters username and password. 3. System validates credentials. 4. User is redirected to the dashboard.
**Alternative Flows:** 1. Incorrect credentials are entered. (User is informed of the error.)

## Use Case 3: View Books
**Preconditions:** User is logged in.
**Postconditions:** User views available books.
**Basic Flow:** 1. User navigates to the books section. 2. System fetches and displays the list of available books.
**Alternative Flows:** 1. No books available. (User sees a message indicating no books available.)

## Use Case 4: Search for a Book
**Preconditions:** User is logged in.
**Postconditions:** User sees search results.
**Basic Flow:** 1. User enters a search query in the search bar. 2. System searches and returns matching books.
**Alternative Flows:** 1. No matches found. (User sees a message indicating no results found.)

## Use Case 5: Add Book to Cart
**Preconditions:** User is logged in and viewing a book's details.
**Postconditions:** Book is added to user's cart.
**Basic Flow:** 1. User clicks on the "Add to Cart" button. 2. System confirms the addition and updates the cart.
**Alternative Flows:** 1. Failed to add due to stock issues. (User is informed.)

## Use Case 6: Checkout
**Preconditions:** User has items in the cart.
**Postconditions:** User completes the purchase.
**Basic Flow:** 1. User navigates to the checkout page. 2. User enters payment details. 3. System processes the payment and confirms the order.
**Alternative Flows:** 1. Payment fails. (User is informed and can retry.)

## Use Case 7: User Profile Update
**Preconditions:** User is logged in.
**Postconditions:** User profile is updated.
**Basic Flow:** 1. User navigates to their profile page. 2. User updates personal information. 3. System saves the updated information.
**Alternative Flows:** 1. Invalid data entered. (User prompted to correct errors.)

## Use Case 8: Logout
**Preconditions:** User is logged in.
**Postconditions:** User is logged out.
**Basic Flow:** 1. User clicks the "Logout" button. 2. System logs the user out and redirects to the login page.
**Alternative Flows:** 1. Session timeout occurs. (User is redirected to the login page automatically.)

