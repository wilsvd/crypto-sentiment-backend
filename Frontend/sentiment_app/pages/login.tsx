import Head from "next/head";
import Link from "next/link";
import styles from "../styles/Home.module.css";
import LoginForm from "../components/login_form";
import Navbar from "../components/navbar";
import Image from "next/image";

import { auth } from "../firebaseConfig";
import { signInWithPopup, GoogleAuthProvider } from "firebase/auth";

function signInGoogle() {
	const provider = new GoogleAuthProvider();
	signInWithPopup(auth, provider)
		.then((result) => {
			// This gives you a Google Access Token. You can use it to access the Google API.
			const credential = GoogleAuthProvider.credentialFromResult(result);
			if (credential) {
				const token = credential.accessToken;
			}
			// The signed-in user info.
			const user = result.user;
			// ...
		})
		.catch((error) => {
			// Handle Errors here.
			const errorCode = error.code;
			const errorMessage = error.message;
			// The email of the user's account used.
			const email = error.customData.email;
			// The AuthCredential type that was used.
			const credential = GoogleAuthProvider.credentialFromError(error);
			// ...
		});
}

export default function LoginPage() {
	return (
		<>
			<Navbar></Navbar>
			<main className={styles.main}>
				<LoginForm></LoginForm>

				<div className="d-grid gap-2">
					<button
						type="button"
						className="btn btn-light"
						onClick={signInGoogle}
					>
						<Image
							src="/google-logo.png"
							alt="Google Logo"
							width={35}
							height={35}
						/>
					</button>
				</div>
			</main>
		</>
	);
}
