# Используем более лёгкий базовый образ
FROM node:18-alpine

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем только package.json и package-lock.json для установки зависимостей
COPY package*.json ./

# Устанавливаем зависимости, используя чистую установку, чтобы избежать кеширования dev-зависимостей в production
RUN npm ci --only=production

# Копируем остальные файлы проекта
COPY . .

# Строим проект
RUN npm run build

# Открываем порт для приложения
EXPOSE 3000

# Запускаем приложение
CMD ["npm", "run", "dev"]
