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


--Balancing tree
get_size Nil = 0
get_size (Node key value nodel noder size) = size

{-
turnLeft Nil = Nil
turnLeft (Node key value nodel noder size) =

turnRight Nil = Nil
turnRight (Node key value nodel noder size) =

swap Nil = Nil
swap (Node key value nodel noder size)
	| get_size nodel - get_size noder > 1 do
	| get_size noder - get_size nodel > 1 = 
	| otherwise = (Node key value nodel noder size)
-}

merge Nil (Node key value nodel noder size) = (Node key value nodel noder size)
merge (Node key value nodel noder size) Nil = (Node key value nodel noder size)
merge Nil Nil = Nil
merge (Node keyF valueF nodelF noderF sizeF) 
	(Node keyS valueS nodelS noderS sizeS) = 
		Node keyS valueS (merge (Node keyF valueF nodelF noderF sizeF) nodelS) noderS (sizeF + sizeS)


insert :: Ord k => k -> v -> BinaryTree k v -> BinaryTree k v
insert k v Nil = Node k v Nil Nil 1
insert k v (Node key value nodel noder size)
	| key == k = Node key v nodel noder size
	| key < k = Node key value (insert k v nodel) noder ((get_size nodel) + (get_size noder) + 1)
	| otherwise = Node key value nodel (insert k v noder) ((get_size nodel) + (get_size noder) + 1)


delete :: Ord k => k -> BinaryTree k v -> BinaryTree k v
delete k Nil = Nil
delete k (Node key value nodel noder size)
	| key == k = merge nodel noder
	| key < k = Node key value (delete k nodel) noder ((get_size nodel) + (get_size noder) + 1)
	| otherwise = Node key value nodel (delete k noder) ((get_size nodel) + (get_size noder) + 1)
