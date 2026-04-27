object MatchingLists {
  def main(args: Array[String]): Unit = {
    
    // This function uses Pattern Matching on a LIST.
    // In Scala, Lists are "Linked Lists". 
    // They are built using two things:
    // 1. 'Nil' -> The empty list (end of the list).
    // 2. '::' (pronounced "Cons") -> Glues an element to the rest of the list.
    //    Example: 1 :: 2 :: 3 :: Nil  is the same as  List(1, 2, 3)

    def describeList(lst: List[Int]): String = lst match {
      
      // Case 1: The list is empty
      case Nil => "Empty list"
      
      // Case 2: The list has exactly one element.
      // x is the head (1st element), Nil is the tail (empty).
      case x :: Nil => s"One element: $x"
      
      // Case 3: The list has exactly two elements.
      // x is 1st, y is 2nd, followed by Nil (empty).
      case x :: y :: Nil => s"Two elements: $x and $y"
      
      // Case 4: The list has at least one element.
      // x is the head (1st element).
      // 'rest' is the tail (EVERYTHING else in the list).
      case x :: rest => s"Starts with $x, has ${rest.length} more elements"
    }

    println(describeList(List()))         // Empty list
    println(describeList(List(1)))        // One element: 1
    println(describeList(List(1, 2)))     // Two elements: 1 and 2
    
    // Matches Case 4: x=1, rest=List(2,3,4)
    println(describeList(List(1,2,3,4)))  // Starts with 1, has 3 more elements
  }
}
