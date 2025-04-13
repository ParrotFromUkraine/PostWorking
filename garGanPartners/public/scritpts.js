//	const swiper = new Swiper('.swiper-container', {
//		loop: true,
//		navigation: {
//			nextEl: '.swiper-button-next',
//			prevEl: '.swiper-button-prev',
//		},
//	})
//

document.querySelector('.burger-menu').addEventListener('click', function () {
	const nav = document.querySelector('.nav')
	const auth = document.querySelector('.auth')
	nav.classList.toggle('active')
	auth.classList.toggle('active')
})