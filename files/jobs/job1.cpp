#include<stdio.h>
#include<conio.h>
#include<string.h>
#include<stdlib.h>

typedef struct
{
    char nume[15];
    char prenume[15];
    int media;
    int grupa;
} informatie;

typedef struct nod
{
    informatie inf;
    struct nod *st,*dr;
} t_nod;


nod *a;

nod *CREARE(nod *rad)
{
    if(rad!=NULL)
    {
        printf("\n Arborele este creat");
        return rad;
    }
    else
    {
        rad=new nod;
        printf(" Numele:");
        scanf("%s",rad->inf.nume);
        printf(" Prenumele:");
        scanf("%s",rad->inf.prenume);
        printf(" Media:");
        scanf("%d",&rad->inf.media);
        printf(" Grupa:");
        scanf("%d",&rad->inf.grupa);
        rad->st=NULL;
        rad->dr=NULL;
        printf("\n Arborele a fost creat");
        return rad;
    }
}
nod *INSERARE(nod *rad, char k[15])
{
    int aux;
    if(rad==NULL)
    {
        rad=new nod;
        strcpy(rad->inf.nume,k);
        printf(" Prenumele:");
        scanf("%s",rad->inf.prenume);
        printf(" Media:");
        scanf("%d",&rad->inf.media);
        printf(" Grupa:");
        scanf("%d",&rad->inf.grupa);
        rad->st=NULL;
        rad->dr=NULL;
        return rad;
    }
    else
    {
        aux=strcmp(rad->inf.nume,k);
        if(aux==0)
        {
            printf("\n Numele acesta exista");
            getch();
            return rad;
        }
        if(aux<0)
            rad->st=INSERARE(rad->st,k);
        else
            rad->dr=INSERARE(rad->dr,k);
    }
    return rad;
}

void LIST(nod *rad)
{
    if(rad)
    {
        LIST(rad->dr);
        {
            printf("\n Numele:%s\n",rad->inf.nume);
            printf(" Prenumele:%s\n",rad->inf.prenume);
            printf(" Media:%d\n",rad->inf.media);
            printf(" Grupa:%d\n",rad->inf.grupa);
        }
        LIST(rad->st);
    }
}


void MODIFICARE(nod *rad, char k[15])
{
    int aux;
    aux=strcmp(rad->inf.nume,k);
    if(aux==0)
    {
        printf(" Prenumele:");
        scanf("%s",rad->inf.prenume);
        printf(" Media:");
        scanf("%d",&rad->inf.media);
        printf(" Grupa:");
        scanf("%d",&rad->inf.grupa);
    }
    else if(aux!=0 && rad->st!=NULL)
        MODIFICARE(rad->st,k);
    else if(aux!=0 && rad->dr!=NULL)
        MODIFICARE(rad->dr,k);
}

nod *DEL(nod *p, nod *q, nod *r)
{
    if(p->dr!=NULL)
        DEL(p->dr,q,r);
    else
    {
        p->dr=r;
        q=q->st;
    }
    return(0);
}


void DELETE(nod *rad, char k[15])
{
    int aux;
    nod *q;
    aux=strcmp(k,rad->inf.nume);
    if(aux<0)
        DELETE(rad->st,k);
    else if(aux>0)
        DELETE(rad->dr,k);
    else
    {
        q=rad;
        if(q->dr==NULL)
            rad=q->st;
        else if(q->st==NULL)
            rad=q->dr;
        else
            DEL(q->st,q,q->dr);
    }
    delete rad;
}

void main()
{
    char ch,litera,k[15];
    do
    {
        clrscr();
        printf("\n 1. Crearea arborelui \n 2. Inserare \n 3. Listare");
        printf("\n 4. Modificare \n 5. Stergere \n 0. Exit \n ");
        ch=getch();
        switch(ch)
        {
        case '1':
            clrscr();
            a=CREARE(a);
            getch();
            break;
        case '2':
            clrscr();
            if(a==NULL)
                printf("\n Trebuie sa creati arborele");
            else
            {
                do
                {
                    clrscr();
                    printf("\n Numele:");
                    scanf("%s",k);
                    INSERARE(a,k);
                    printf("\n Continuati?");
                    litera=getch();
                }
                while((litera!='n')&&(litera!='N'));
            }
            getch();
            break;
        case '3':
            clrscr();
            if(a==NULL)
                printf("\n Trebuie sa creati arborele");
            else
            {
                clrscr();
                LIST(a);
            }
            getch();
            break;
        case '4':
            clrscr();
            if(a==NULL)
                printf("\n Trebuie sa creati arborele");
            else
            {
                printf("\n Numele:");
                scanf("%s",k);
                MODIFICARE(a,k);
            }
            getch();
            break;
        case '5':
            clrscr();
            if(a==NULL)
                printf("\n Trebuie sa creati arborele");
            else
            {
                printf("\n Numele:");
                scanf("%s",k);
                DELETE(a,k);
                printf("\n Nodul a fost sters");
            }
            getch();
            break;
        }
    }
    while(ch!='0');
}




Acesta e codul la stergere:
nod *DEL(nod *p, nod *q, nod *r)
{
    if(p->dr!=NULL)
        DEL(p->dr,q,r);
    else
    {
        p->dr=r;
        q=q->st;
    }
    return(0);
}


void DELETE(nod *rad, char k[15])
{
    int aux;
    nod *q;
    aux=strcmp(k,rad->inf.nume);
    if(aux<0)
        DELETE(rad->st,k);
    else if(aux>0)
        DELETE(rad->dr,k);
    else
    {
        q=rad;
        if(q->dr==NULL)
            rad=q->st;
        else if(q->st==NULL)
            rad=q->dr;
        else
            DEL(q->st,q,q->dr);
    }
    delete rad;
}
