# Django E-Commerce Website

![Gif](https://imgur.com/80Vdf5i)

This is an E-commerce project for my university's database course where users can shop and sell products. A very basic shopping system has been implemented in a very short time period so expect some bugs.

**Features:**
- User Authentication/Registration
- Shop Creation
- Product Listing
- Product Searching
- Add to cart function
- Payment gateway
- Downloading order information in CSV format
- Updatability of everything


## Running the Project
- Remove sqlite.db as it does not have the required media files which might give error
- Create a virtual environment and 'pip install -r requirements.txt'
- Create an environment variable '.env' in the root directory containing Stripe's private key
- Run: 'python manage.py runserver'