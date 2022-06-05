# Hash Crush
Inspired by [Amir's](https://github.com/amirgamil/) [ZK-Crush](https://github.com/amirgamil/zk-crush)

Hash Crush is an anonymous (though [not technically zk](https://crypto.stackexchange.com/questions/70877/is-a-hash-a-zero-knowledge-proof)) approach to telling your crush you like them.

## Improvements over zk-crush
- Sender and recipient both anonymized (both are hashed). Great for posting on a confessions page or other public board.
- Hashes are salted and whitespace is trimmed; resistant to rainbow table attacks like [ZK-Crush-Break](https://github.com/verumlotus/ZK-Crush-Break)
- Ability to add multiple crushes
- Group-crush mode - great for speed dating or events (used by [Mingle DAO](https://twitter.com/mingledao))

## How to use it
### Individual mode
Individual mode is link-based, and does not store any data. After entering your name as well as the name of your crush(es), a link is generated which can be shared.
<img width="1129" alt="image" src="https://user-images.githubusercontent.com/58539993/172073016-23ffbaa3-20c9-40c2-b4ce-b61a97e6d493.png">

When the URL is visited, their name and crushes are compared against the name and crushes in the link and a result is displayed.

<img width="1141" alt="image" src="https://user-images.githubusercontent.com/58539993/172073033-6c94e264-72bd-43d3-b1f2-b13c6f59b512.png">

### Group mode
Group mode is based on a "Group ID". The first time a Group ID is used, a warning is displayed; if you are looking to create a new Group ID and there is no warning, this indicates the Group ID is taken. After creating a Group ID, share it with other participants, they must enter the same Group ID. Crush names are stored in the browser's local cookies; those with strict privacy settings may want to screenshot them for posterity (only a number will be provided if names are not found in cookies). Salted hashes are stored in our database; these are anonymous and secure.

<img width="1131" alt="image" src="https://user-images.githubusercontent.com/58539993/172073055-43bd1856-f36d-4580-ba04-a050028d44bb.png">

After everyone has submitted, proceed to enter your Group ID and name into the results page, where they will be compared against others in the database. 

<img width="1142" alt="image" src="https://user-images.githubusercontent.com/58539993/172073085-88aa402a-d407-49a9-8481-154bd81c4065.png">