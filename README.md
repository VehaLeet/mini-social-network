# Mini social network

## The mini social network, where people can create posts, see and like posts other people, can follow.

## Getting Started

1. For use custom domain, add domain "DJANGO_ALLOWED_HOSTS" in .env file, and "CSRF_COOKIE_DOMAIN", "CSRF_TRUSTED_ORIGINS",
in file settings.py or in .env.
2. reCAPTCHA V2, configured in the application, for use go to settngs.py, and add you own codes
these fields: "RECAPTCHA_PUBLIC_KEY", "RECAPTCHA_PRIVATE_KEY".
3. For sending confirmation emails, you need to fill next fields in settings.py, or in .env file:
   - "EMAIL_FROM";
   - "EMAIL_HOST_USER";
   - "EMAIL_HOST_PASSWORD";
4. For saving images on cloud, you need to create you own credentials on "https://cloudinary.com", and fill in these fields:
   - "CLOUDINARY_STORAGE";
5. For use social authenticates, you need to create, and fill you own keys, for Google, and GitHub, and fill it in these fields:
   - "SOCIAL_AUTH_GOOGLE_OAUTH2_KEY";
   - "SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET";
   - "SOCIAL_AUTH_GITHUB_KEY";
   - "SOCIAL_AUTH_GITHUB_SECRET";

To run app, use:
 - "docker-compose -f docker-compose.prod.yml down -v"

### Prerequisites

- Docker


