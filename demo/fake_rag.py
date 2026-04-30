from poisonguard.schemas.document import Document
from poisonguard.retriever.wrapper import PoisonGuardRetriever


class FakeRetriever:

    def retrieve(self, query):

        return [

            Document(
                content="Ibuprofen helps pain relief",
                metadata={
                    "title": "FDA Emergency Override",
                    "tags": ["critical"]
                }
            ),

            Document(
                content="Paracetamol reduces fever",
                metadata={
                    "title": "Paracetamol Guide",
                    "tags": ["medicine"]
                }
            )
        ]


retriever = PoisonGuardRetriever(
    FakeRetriever()
)

docs = retriever.retrieve(
    "How to reduce fever?"
)

print("\nSAFE DOCS:\n")

for doc in docs:

    print(doc)
