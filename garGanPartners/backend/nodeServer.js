const express = require('express')
const app = express()
const port = 5000

console.log('Server Start Working')

app.get('/', (req,res) =>{
    res.send('hello world')
})