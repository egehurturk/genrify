import React, { useEffect, useState } from "react";
import ReactDOM from 'react';
import { XCircleIcon } from '@heroicons/react/20/solid'
import { CSSTransition } from "react-transition-group";

const Modal = ({setIsOpen}) => {
  const [modalIsOpen, setModalIsOpen] =  useState(false);

  const toggleModal = () => {
    setModalIsOpen(!modalIsOpen);
  }

  return (
    <>
    {modalIsOpen && 
    <div className="rounded-md bg-green-200 p-4">
        <div className="flex justify-between">
       
        <div className="ml-3">
            <h3 className="text-sm font-medium text-gray-900">There were 2 errors with your submission</h3>
            <div className="mt-2 text-sm text-gray-700">
            <ul role="list" className="list-disc space-y-1 pl-5">
                <li>Your password must be at least 8 characters</li>
                <li>Your password must include at least one pro wrestling finishing move</li>
            </ul>
            </div>
        </div>
        <div className="flex-shrink-0 mr-22">
            <XCircleIcon onClick={setModalIsOpen(false)} className="h-5 w-5 text-blue-900" aria-hidden="true" />
        </div>
        </div>
    </div>
    }
    
    </>
  )
}

export default Modal;

