CXX = g++
CXXFLAGS = -std=c++17 -Wall -Wextra
LIBS = -lsqlite3
TARGET = score
SRC = main.cpp db.cpp scoring.cpp
OBJ = $(SRC:.cpp=.o)
HEADERS = $(wildcard *.h)

# Link step: join the object files into the final executable
$(TARGET): $(OBJ)
	$(CXX) $(CXXFLAGS) $(OBJ) -o $(TARGET) $(LIBS)

# Compile step: each .cpp -> its own .o (rebuilt if the .cpp or any header changes)
%.o: %.cpp $(HEADERS)
	$(CXX) $(CXXFLAGS) -c $< -o $@

.PHONY: clean
clean:
	rm -f $(TARGET) $(OBJ)
