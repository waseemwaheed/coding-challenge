# Coding challenge solution

## Assumptions
* One input file can be consumed at a time.
* The frequency at which updates arrive is fixed (1s). Hence the average, in the general case, is taken over 300 samples.
* A single stream (input file) can contain more than one currency pair.

## Decisions
* The solution is written in Python and the reason is that I am more comfortable with language at this point.
* Testing is done in pytest. Ease of use and familiarity are the reasons for this choice.
* To keep track of the exchange rates for each pair, I made the currency pairs keys of a dictionary which maps to sliding window [deque](https://docs.python.org/3/library/collections.html#collections.deque) data structure.
  * The rationale behind choosing a dictionary is because, each new line can be new data point for a currency pair, which means the currency pairs data need to be accessed in random order and a dictionary is the best options here where an access operation is $O(1)$
  * The rationale behind choosing a deque is that it allows for the easy creation of a sliding window. A deque has $O(1)$ complexity when we append to or access the ends of the queue, which is what we are doing here.

* The `CurrencyPairData` class is a subclass of the `Observable` class. This allows me to easily add callbacks to `CurrencyPairData` instances. 

## Execution
The code runs in a docker container which means [docker](https://www.docker.com/) should be installed for the code to run. To run the code, follow the steps in a shell:

**Note : to able to run on your own \*.jsonl files, copy the files to the examples directory before following the steps. The files input1.jsonl through to input6.jsonl are already there and they are part of the unit testing.**
1. change directory to where the files are stored
2. Build the docker image by running: 
    ```bash
    docker build -t awc_image .
    ```
3. Instantiate a docker container by running: 
   ```bash
    docker run -it --name cc_container --rm --volume $(pwd)/src/:/coding_challenge/src/ --volume $(pwd)/example/:/coding_challenge/example/ cc_image:latest sh
   ```

   To run unit tests:
      ```bash
      pytest
      ```
   Otherwise, to run the code on one of the files in the example directory:
   ```bash
   python src/main/main.py example/<test_file>
   ```

 

4. Finally and once done and after exiting the container, to delete the image built in step 1:
   ```bash
   docker rmi cc_image
   ```