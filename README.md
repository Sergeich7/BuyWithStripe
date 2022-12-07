## BuyWithStripe
Прием онлайн платежей через STRIPE. Платежи производятся как методом Session, так и PaymentIntent. Реализована возможность использования купонов и автоматическое удержание налогов.

### При разработки использовал
Python, Django, Stripe, SQLite, Docker, Docker compose.

### Установка и запуск

* git clone https://github.com/Sergeich7/BuyWithStripe.git
* cd BuyWithStripe
* Необходимо создать файл .env на основе .env.sample с вашими ключами от STRIPE

Docker:
* docker build . -t buywithstripe
* docker run -d --env-file .env --rm --name BuyWithStripe -p 8137:8000 buywithstripe

или Docker compose:
* docker-compose up --build -d

### Сайт
* http://localhost:8137/
* http://localhost:8137/admin (admin/admin)

