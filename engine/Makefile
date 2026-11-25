CXX = g++
CXXFLAGS = -std=c++17 -Wall -Wextra
LIBS = -lsqlite3
TARGET = score
SRC = main.cpp db.cpp
OBJ = $(SRC:.cpp=.o)

# Link step: join the object files into the final executable
$(TARGET): $(OBJ)
	$(CXX) $(CXXFLAGS) $(OBJ) -o $(TARGET) $(LIBS)

# Compile step: each .cpp -> its own .o (rebuilt if the .cpp or db.h changes)
%.o: %.cpp db.h
	$(CXX) $(CXXFLAGS) -c $< -o $@

.PHONY: clean
clean:
	rm -f $(TARGET) $(OBJ)
