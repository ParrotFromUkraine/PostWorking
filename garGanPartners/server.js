const express = require('express')
const path = require('path')

const app = express()
const port = 5000

// Раздача статических файлов из папки "public"
app.use(express.static(path.join(__dirname, 'public')))

// Отображение главной страницы
app.get('/', (req, res) => {
	res.sendFile(path.join(__dirname, 'public', 'index.html'))
})

// Запуск сервера
app.listen(port, () => {
	console.log(`Сервер запущен на http://localhost:${port}`)
})
