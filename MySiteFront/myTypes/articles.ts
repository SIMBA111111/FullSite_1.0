// articles.ts
export type ArticlesWithAuthor = {
    id: number;
    name: string;
    text: string;
    main_text: string;
    article_datetime: string;
    slug: string;
    article_author: {
        id: number;
        first_name: string;
        last_name: string;
    };
};