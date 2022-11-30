import Image from "next/image";

export default function CryptoTable() {
	return (
		<table className="table">
			<thead>
				<tr>
					<th scope="col"></th>
					<th scope="col">#</th>
					<th scope="col">Name</th>
					<th scope="col">Symbol</th>
					<th scope="col">Sentiment</th>
					<th scope="col">Last 7 Days</th>
				</tr>
			</thead>
			<tbody>
				<tr>
					<th scope="row">
						<Image
							src="/favourite_icon.png"
							alt="Favourite Logo"
							width={35}
							height={35}
						></Image>
					</th>
					<td>1</td>
					<td>Bitcoin</td>
					<td>BTC</td>
					<td>0.7</td>
					<td>TO BE ADDED</td>
				</tr>
				<tr>
					<th scope="row">
						<Image
							src="/favourite_icon.png"
							alt="Favourite Logo"
							width={35}
							height={35}
						></Image>
					</th>
					<td>2</td>
					<td>Ethereum</td>
					<td>ETH</td>
					<td>0.0</td>
					<td>TO BE ADDED</td>
				</tr>
				<tr>
					<th scope="row">
						<Image
							src="/favourite_icon.png"
							alt="Favourite Logo"
							width={35}
							height={35}
						></Image>
					</th>
					<td>3</td>
					<td>BNB</td>
					<td>BNB</td>
					<td>-0.7</td>
					<td>TO BE ADDED</td>
				</tr>
			</tbody>
		</table>
	);
}
