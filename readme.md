# Hash Crush
Inspired by [Amir's](https://github.com/amirgamil/) [ZK-Crush](https://github.com/amirgamil/zk-crush)

However, I wanted to have both the sender and the recipient to be anonymized - thus, both are hashed and checked against each other. In addition, whitespace is trimmed and the hash is salted (like a password, to prevent rainbow table attacks).