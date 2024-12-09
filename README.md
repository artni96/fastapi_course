# fastapi_course
docker network create booking_network

docker run --name booking_db \
    -p 6432:5432 \
    -e POSTGRES_USER=postgres \
    -e POSTGRES_PASSWORD=postgres \
    -e POSTGRES_DB=booking \
    --network=booking_network \
    --volume pg-booking-data:/var/lib/postgresql/data \
    -d postgres:16

docker run --name booking_cache \
    -p 7379:6379 \
    --network=booking_network \
    -d redis:7.4

docker run --name booking_backend \
    -p 7777:8000\
    --network=booking_network \
    booking_image
    

docker build -t booking_image .

docker run --name booking_nginx \
    --volume ./nginx.conf:/etc/nginx/nginx.conf \
    --network=booking_network \
    --rm -p 80:80 nginx