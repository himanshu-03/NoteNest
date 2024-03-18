const signUpButton = document.getElementById("signUp");
		const signInButton = document.getElementById("signIn");
		const container = document.getElementById("container");
		
		signUpButton.addEventListener('click',()=>{
			container.classList.add("right-panel-active");
		})

		signInButton.addEventListener('click',()=>{
			container.classList.remove("right-panel-active");
		})

document.getElementById('signUp').addEventListener('click', function() {

	document.querySelector('.signin').style.display = 'none';
	
	document.querySelector('.signup').style.display = 'block';
});

document.getElementById('signIn').addEventListener('click', function() {

	document.querySelector('.signin').style.display = 'block';
});