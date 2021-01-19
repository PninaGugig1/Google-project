from project.offline import offline
from project.online import online

if __name__ == "__main__":
    trie = offline()
    online(trie)

