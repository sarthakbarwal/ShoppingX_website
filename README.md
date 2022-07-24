In this project, I have developed an e-commerce website 'ShoppingX' using Django, HTML, CSS, JavaScript, Python, and Ajax. It has Customer Registration, Login, Password Reset, Profile, Orders, Add to Cart, Quantity Update, Live Sale, and more, but no payment gateway system. 

Going on the models and structures in this project, we get a default User Model from Django. Other than this, I have made four more models: Customer, Product, Order placed, and Cart. The Customer model has six fields, user, name, locality, city, zip code, and state. The product model has seven fields, title, selling_price, discounted_price, description, brand, category, and prodcut_image. The order placed model has six fields, user, customer, quantity, ordered_date, and status and the Cart model has three fields, user, product, and quantity. These models have relations; the user model has many to one relation with customer, orderplaced, and cart model. The orderplaced model also has many to one relation with the customer and product model, and lastly, the cart model has many to one relation with the product model.

I have downloaded all the images in this project from "https://unsplash.com/," and the prices and names of these products are arbitrary. The Website also has a forget password option, and I have made it so that when the user will proceed to this option, the link to reset the password will be sent on the console and not on the actual email-id. To get a responsive website, I have also written some Java and CSS script, the rest of the CSS and JavaScript is used from "https://getbootstrap.com/docs/5.1/getting-started/introduction/".

The 'app' folder has all the main code files including templates sale product images.

The 'media' folder has all the proucts images.

The 'shopping' folder has inbuilt Django files including settings file.
