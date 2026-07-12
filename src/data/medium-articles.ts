import type { MediumArticle } from '../utils/medium-feed';

export const curatedMediumArticles: MediumArticle[] = [
  {
    title: 'Post Morten',
    url: 'https://medium.com/@santiagogonzalezcuellar/post-morten-14d925acff9e',
    date: new Date('2023-08-01T00:28:08.000Z'),
    excerpt:
      'In software development or IT support, a post-mortem report documents how a process failed, what was learned, and how similar problems can be avoided.',
    thumbnail: '/images/posts/medium-post-morten-blog.png',
    categories: ['retrospectives', 'software-testing', 'postmortem-documentation'],
  },
  {
    title: 'Cost-Savings From the Use of the Biosimilars in Slovakia',
    url: 'https://medium.com/@santiagogonzalezcuellar/cost-savings-from-the-use-of-the-biosimilars-in-slovakia-4f64030a08ef',
    date: new Date('2023-04-07T21:12:05.000Z'),
    excerpt:
      'A short article based on research about the potential cost savings from the use of biosimilars in Slovakia.',
    thumbnail: '/images/posts/medium-sk-blog.png',
    categories: ['biosimilars'],
  },
  {
    title: 'Hash Functions',
    url: 'https://medium.com/@santiagogonzalezcuellar/hash-functions-33043182ddc2',
    date: new Date('2023-03-29T04:13:52.000Z'),
    excerpt:
      'A hash function takes input data and produces a fixed-size output known as a hash value or digest.',
    thumbnail: '/images/posts/medium-hashfunctions-blog.png',
    categories: ['hashing'],
  },
  {
    title: 'Symmetric Cryptography',
    url: 'https://medium.com/@santiagogonzalezcuellar/symmetric-cryptography-635ea10bf108',
    date: new Date('2023-03-26T22:07:13.000Z'),
    excerpt:
      'Notes on symmetric cryptography, where the same secret key is used for encryption and decryption.',
    thumbnail: '/images/posts/medium-cryptography-blog.png',
    categories: ['symmetric-encryption'],
  },
  {
    title: 'Encrypting File System',
    url: 'https://medium.com/@santiagogonzalezcuellar/encrypting-file-system-49ac62ab979a',
    date: new Date('2023-03-02T03:15:56.000Z'),
    excerpt:
      'A study note about EFS, the Encrypting File System, and how file encryption relates to system security.',
    thumbnail: '/images/posts/medium-encrypting-file-system-blog.png',
    categories: ['active-directory-security'],
  },
  {
    title: 'Active Directory',
    url: 'https://medium.com/@santiagogonzalezcuellar/active-directory-f2933ed55604',
    date: new Date('2023-02-28T02:55:31.000Z'),
    excerpt:
      'Notes from IT support studies about Active Directory, directory services, and Windows administration basics.',
    thumbnail: '/images/posts/medium-active-directory-blog.png',
    categories: ['active-directory'],
  },
];
