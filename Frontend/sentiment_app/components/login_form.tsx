import Head from "next/head";
import Image from "next/image";
import Link from "next/link";

export default function LoginForm() {
	return (
		<div>
			<form>
				<div className="mb-3">
					<label htmlFor="exampleInputEmail1" className="form-label">
						Email address
					</label>
					<input
						type="email"
						className="form-control"
						id="exampleInputEmail1"
						aria-describedby="emailHelp"
					></input>
				</div>
				<div className="mb-3">
					<label
						htmlFor="exampleInputPassword1"
						className="form-label"
					>
						Password
					</label>
					<input
						type="password"
						className="form-control"
						id="exampleInputPassword1"
					></input>
				</div>
				<div className="d-grid gap-2">
					<button type="submit" className="btn btn-primary">
						Login
					</button>
				</div>
			</form>
		</div>
	);
}
