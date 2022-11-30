import { useState, useEffect } from "react";

export default function Profile() {
	const [data, setData] = useState(null);
	const [isLoading, setLoading] = useState(false);

	useEffect(() => {
		setLoading(true);
		fetch("http://localhost:8000/")
			.then((res) => res.json())
			.then((data) => {
				setData(data);
				setLoading(false);
			});
	}, []);

	if (isLoading) return <p>Loading...</p>;
	if (!data) return <p>No profile data</p>;

	return (
		<div>
			{Object.entries(data).map(([key, value]) => {
				return (
					<div key={key}>
						<h2>
							{key}: {data[key].sentiment}
						</h2>

						<hr />
					</div>
				);
			})}
		</div>
	);
}
