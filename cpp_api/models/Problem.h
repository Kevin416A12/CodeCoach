//
// Created by kevin on 27/10/25.
//

#pragma once
#include <string>
#include <bsoncxx/builder/stream/document.hpp>
#include <bsoncxx/json.hpp>

class Problem {
public:
    std::string title;
    std::string description;
    std::string inputExample;
    std::string outputExample;

    bsoncxx::document::value toBson() const {
        using namespace bsoncxx::builder::stream;
        return document{}
                << "title" << title
                << "description" << description
                << "inputExample" << inputExample
                << "outputExample" << outputExample
                << finalize;
    }
};
