import Prelude hiding (lookup)

data BinaryTree k v = Nil
	| Node k v (BinaryTree k v) (BinaryTree k v) Int
	deriving (Show, Eq, Ord)

lookup :: Ord k => k -> BinaryTree k v -> Maybe v
lookup k Nil = Nothing
lookup k (Node key value nodel noder size)
	| key == k = Just value
	| key < k = lookup k $ nodel
	| otherwise = lookup k $ noder

{-
--Balancing tree
get_size Nil = 0
get_size (Node key value nodel noder size) = size

turnLeft Nil = Nil
turnLeft (Node key value nodel noder size) =

turnRight Nil = Nil
turnRight (Node key value nodel noder size) =

swap Nil = Nil
swap (Node key value nodel noder size)
	| get_size nodel - get_size noder > 1 = 
	| get_size noder - get_size nodel > 1 = 
	| otherwise = (Node key value nodel noder size)
-}


makeNode Nil (Node key value nodel noder size) k v = Node k v Nil (Node key value nodel noder size) (size + 1)
makeNode (Node key value nodel noder size) Nil k v = Node k v (Node key value nodel noder size) Nil (size + 1)
makeNode Nil Nil k v = Node k v Nil Nil 1
makeNode (Node keyF valueF nodelF noderF sizeF) 
	(Node keyS valueS nodelS noderS sizeS) k v = 
		Node k v (Node keyF valueF nodelF noderF sizeF) (Node keyS valueS nodelS noderS sizeS) (sizeF + sizeS + 1)

merge Nil (Node key value nodel noder size) = (Node key value nodel noder size)
merge (Node key value nodel noder size) Nil = (Node key value nodel noder size)
merge Nil Nil = Nil
merge (Node keyF valueF nodelF noderF sizeF) 
	(Node keyS valueS nodelS noderS sizeS) = 
		Node keyS valueS (Node keyF valueF nodelF noderF sizeF) (merge nodelS noderS) (sizeF + sizeS)


insert :: Ord k => k -> v -> BinaryTree k v -> BinaryTree k v
insert k v Nil = Node k v Nil Nil 1
insert k v (Node key value nodel noder size)
	| key == k = Node key v nodel noder size
	| key < k = makeNode (insert k v nodel) noder key value
	| otherwise = makeNode nodel (insert k v noder) key value


delete :: Ord k => k -> BinaryTree k v -> BinaryTree k v
delete k Nil = Nil
delete k (Node key value nodel noder size)
	| key == k = merge nodel noder
	| key < k = makeNode (delete k nodel) noder key value
	| otherwise = makeNode nodel (delete k noder) key value
