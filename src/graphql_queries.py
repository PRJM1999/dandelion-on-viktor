# This file contains GraphQL queries as string constants

GET_STREAMS_QUERY = """
    query Streams($cursor: String) {
        streams(cursor: $cursor, limit: 50) {
            cursor
            items {
                id
                name
                description
                role
                isPublic
                createdAt
                updatedAt
                commentCount
                collaborators {
                    id
                    name
                    company
                    avatar
                    role
                }
                commits(limit: 1) {
                    items {
                        id
                        createdAt
                        message
                    }
                }
                branches {
                    items {
                        id
                        name
                        commits {
                            items {
                                id
                                authorName
                                createdAt
                                message
                                referencedObject
                                branchName
                                sourceApplication
                            }
                        }
                    }
                }
            }
        }
    }
"""
