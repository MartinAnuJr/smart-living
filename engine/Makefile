CXX = g++
CXXFLAGS = -std=c++17 -Wall -Wextra
LIBS = -lsqlite3
TARGET = score
SRC = main.cpp

$(TARGET): $(SRC)
	$(CXX) $(CXXFLAGS) $(SRC) -o $(TARGET) $(LIBS)

.PHONY: clean
clean:
	rm -f $(TARGET)
