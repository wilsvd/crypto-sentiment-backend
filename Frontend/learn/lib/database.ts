import { ref, set, onValue, remove } from "firebase/database";
import { database } from "../firebaseConfig";

const db = database;

export function writeUserData(userId: any, name: any, email: any) {
  set(ref(db, "users/" + userId), {
    username: name,
    email: email,
  });
}

export function readUserData() {
  const data = ref(db, "users/");
  onValue(data, (snapshot) => {
    const my_data = snapshot.val();
    if (my_data) {
      Object.values(my_data).forEach((value) => {
        console.log(value);
      });
    } else {
      console.log("Object is falsy");
    }
  });
}

export function deleteUserData(userId: any) {
  const data = ref(db, "users/" + userId);

  remove(data)
    .then(() => {
      console.log("Data deleted");
    })
    .catch((error) => {
      console.log(error);
    });
}
