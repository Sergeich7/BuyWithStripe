Прием онлайн платежей через STRIPE.
Платежи производятся как методом Session, так и PaymentIntent.
Реализована возможность использования купонов и автоматическое удержание налогов.

При разработке использовал Python, Django, Stripe, SQLite, Docker, Docker compose.

Код проекта:
https://github.com/Sergeich7/BuyWithStripe

Адрес сайта:
http://buywithstripe.artgallery-tatyana.ru/

Адмика:
http://buywithstripe.artgallery-tatyana.ru/admin/

Также можно запустить приложение в контейнере

git clone https://github.com/Sergeich7/BuyWithStripe.git
cd BuyWithStripe

Необходимо создать файл .env на основе .env.sample с вашими ключами от STRIPE

Docker:
docker build . -t buywithstripe
docker run -d --env-file .env --rm --name BuyWithStripe -p 8000:8000 buywithstripe

или Docker compose:
docker-compose up --build -d
