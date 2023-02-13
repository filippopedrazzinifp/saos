# SaoS - Streamlit Auth OpenAI Stripe

This is a template for creating complete web apps with Streamlit, Authentication, OpenAI, and Stripe. It provides an easy way to get started with building a POC, but having all the main functionalities of a State of the art SaaS application.

## Running the App Locally or in Production

0. Create a Stripe account and enable payment links https://stripe.com/docs/payments/payment-links. When customizing the checkout, use the advanced option and provide the redirect URL to your custom domain.
1. Create a Customer Portal https://dashboard.stripe.com/settings/billing/portal enabling the possibility for your users to cancel the subscription.
2. Create a `.env` file including the following environment variables

```
OPENAI_API_KEY=
CUSTOM_DOMAIN=
STRIPE_SECRET_KEY=
STRIPE_PAYMENT_URL=
STRIPE_BILLING_URL=
```

3. Create an `auth.yaml` file that will contain all the users. Use the following format:

```yaml
cookie:
  expiry_days: 30
  key: changeme
  name: auth_cookie
credentials:
  usernames:
    admin:
      email: example@example.com
      name: admin
      password: hashed_password
preauthorized:
  emails:
    - example@example.com
```

> In order to handle authentication, we are using streamlit-authenticator package. Please refer to this link in order to create an hashed password: https://github.com/mkhorasani/Streamlit-Authenticator

4. Run the app with `docker-compose`

```bash
docker-compose up --build -d
```

## Demo

You can check a working web app at https://app-tlria.joandko.io

<video src="./assets/saos.mp4" width=auto/>

![demo](./assets/saos.gif)

## License

This project is licensed under the MIT License.
